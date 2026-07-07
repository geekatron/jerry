# Steelman Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable identification and scope |
| [Summary](#summary) | Charitable assessment and improvement count |
| [Charitable Reading (H-16 First Pass)](#charitable-reading-h-16-first-pass) | The strongest case for this ADR, stated before any critique |
| [Steelman Reconstruction](#steelman-reconstruction) | Targeted strengthening patches (not a full rewrite -- see rationale) |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Full before/after/rationale per Major finding |
| [Scoring Impact](#scoring-impact) | Dimension-level effect of incorporating these improvements |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
- **Deliverable Type:** ADR (Nygard format, L0/L1/L2)
- **Criticality Level:** C3 (per commission; AE-003 auto-C3 minimum for new ADRs)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (S-003) | **Date:** 2026-07-07 | **Original Author:** ps-architect
- **Review round:** iteration-005 (this ADR's 5th tournament pass; changelog shows 4 prior remediation cycles, v0.1 -> v0.5)

---

## Summary

**Steelman Assessment:** This is an unusually mature deliverable for a first-pass review target -- it has already absorbed four rounds of disclosed, cited, self-correcting remediation (its own changelog documents DA-/CC-/CV-/SM-tagged fixes through iteration-4), and it already performs a form of internal steelmanning (each Options-Considered decision steelmans its strongest rejected alternative before choosing). The core thesis -- that an independent 3-lens refutation panel is the load-bearing fix for a demonstrated additive-remediation spiral -- is well-evidenced, its cost model is internally consistent, and every citation spot-checked against the evidence corpus during this review resolved exactly as claimed (see verification note below). The genuine remaining gaps are narrow: a handful of places where the document's own high bar for concreteness (numeric triggers, quoted evidence, operational test definitions) is not applied as consistently as it is everywhere else.

**Improvement Count:** 0 Critical, 5 Major, 1 Minor

**Original Strength:** HIGH. No fundamental thesis defect found. All identified gaps are presentation/completeness/specification gaps in an already-strong argument, not substantive flaws in the decision.

**Recommendation:** Incorporate improvements (targeted). The reconstruction below is additive patches at named insertion points, not a wholesale rewrite -- consistent with the ADR's own D-3 subtraction-first doctrine, adding the minimum text needed to close each gap rather than restructuring sections that already work.

**Verification note (P-022, spot-check performed during this Steelman pass, not merely charitable assumption):** `skills/adversary/agents/adv-scorer.md:166-167` matches the ADR's quotation verbatim ("Any Critical finding from adv-executor reports -> automatic REVISE regardless of score" / "Score >= 0.92 but with unresolved Critical findings -> REVISE"). `skills/adversary/agents/adv-selector.md:109-128` matches the ADR's Group A-F ordering and the H-16 constraint statement exactly. The cited panel-file counts were independently re-derived by filesystem enumeration: `.../adr-convention-20260702-001/adversary/iteration-009/verify/` returns exactly 15 files (3 lenses x 5 Critical-bearing reports: s-001, s-002, s-004, s-011, s-012), and `.../fu-log-convention-20260705-001/adversary/iteration-008/verify/` returns exactly 12 files (3 lenses x 4 reports: s-001, s-002, s-004, s-012) -- both match the ADR's stated figures exactly. This gives the charitable reading below a factual, not merely assumed, foundation.

---

## Charitable Reading (H-16 First Pass)

Before any gap is named, the strongest version of this ADR's case, stated plainly:

The record is about as clean as observational evidence in this domain gets: two independently-run C4 governance packages, 18 rounds, a repeatedly-observed failure signature (zero regressions + a constant fresh-Critical rate + a flat-or-declining composite), a single structural intervention introduced mid-engagement, and a repeated, large, same-direction effect (+0.18 to +0.21 composite) every time that intervention ran. The document does not merely assert this pattern -- it names the exact rounds, quotes the exact scorer language, and (per the disclosed corrections in the changelog) has already caught and fixed its own citation errors, including a genuinely embarrassing one (a fabricated "Glob-verified" absence claim) that it uses as the central cautionary tale for the very discipline it is proposing. That the document turns its own worst evidentiary near-miss into the strongest argument for verifier independence is a mark of intellectual honesty, not a defect to be steelmanned away.

The six decisions (D-1 through D-6) are coherent as a single design: independence is the property that did the work (Force 6), so status-quo and scorer-side verification are correctly ruled out; the C1-C2 exemption is honestly labeled a cost default rather than an empirical finding, which is exactly the right epistemic humility given the record is 100% C4; and the remediation/stop-condition/continuity decisions (D-3, D-4, D-5) are the minimum scaffolding the verify stage needs to be coherent, not scope creep. The cost model is priced in the framework's own native unit (tokens, not just invocation counts) and is honest that the invocation-count figure is a lower bound. Given all of this, the residual gaps below are opportunities to make an already-strong specification fully implementable, not indictments of the decision itself.

---

## Steelman Reconstruction

Given the maturity noted above, the reconstruction is presented as five targeted insertions at named locations, each closing one SM-NNN gap, rather than a line-by-line rewrite of the whole 1,095-line document. Full text for each insertion is in [Improvement Details](#improvement-details).

1. **After L1 item 1's invocation-contract bullet** (deliverable line ~736, "Default rule: REFUTED on uncertainty") -- add one sentence defining the lens-failure fallback (SM-001).
2. **In RSK-6's mitigation cell** (deliverable line ~947) -- replace "once the team is calibrated" with a concrete, numeric sunset trigger mirroring the Phase-2 trigger already used in L2 (SM-002).
3. **In D-4's decision row or a new D-4 sub-bullet** (deliverable lines ~418, ~490) -- add an operational definition of "recurrence" (same file+line + same defect class across independent rounds, distinct wording permitted) so WI-6's runner guide and WI-8's falsification test have a testable criterion (SM-003).
4. **In L1 item 1 or item 2** (deliverable lines ~732-735, ~752-769) -- quote one real 3-5 line verdict excerpt from the cited evidence (e.g., `.../iteration-009/verify/s-001-refutation-factual.md`) so the panel-file format is demonstrated, not only narrated (SM-004).
5. **In Fig. 3's SWITCH node or Forces #2** (deliverable lines ~289-292, ~634-635) -- add an explicit user-notification step when the tournament switches from the old (cheap) to the verified (order-of-magnitude costlier) protocol, mirroring the mandatory escalation already required at the RT-M-010 ceiling (SM-005).

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|---------------|-----------|
| SM-001-iter5 | No fallback rule for a lens invocation that errors or fails to return a verdict (partial panel) | Major | "2-of-3 majority, blind to each other... Default rule: REFUTED on uncertainty" (Decision D-1 row, L1 item 1) -- silent on missing/failed lens runs | Add: "A lens invocation that errors or fails to return a verdict counts as a REFUTED vote for that lens (consistent with DEFAULT-REFUTED); the panel proceeds with the remaining verdicts under the same 2-of-3 rule." | Methodological Rigor / Actionability |
| SM-002-iter5 | Dual-protocol sunset trigger is judgment-only where an adjacent trigger in the same document is numeric | Major | RSK-6 mitigation: "Operative verdict always labeled; sunset the old-protocol composite once the team is calibrated." | Add a concrete trigger, e.g.: "...once N consecutive C3/C4 rounds (N=3, mirroring the Phase-2 trigger window) show no material divergence between the verified and old-protocol composites." | Actionability / Internal Consistency |
| SM-003-iter5 | "Recurrence across independent rounds" (the D-4 convergence discriminator) is illustrated by one example but never operationally defined | Major | D-4: "Recurrence across *independent* rounds marks a real defect... a fresh non-overlapping crop every round marks a protocol artifact" -- no test given for what counts as the same recurring item | Add an explicit test: "A finding recurs when a subsequent independent round's finding cites the same file+line span (or an overlapping span) and the same defect class, even if the wording or finding ID differs; distinct wording alone does not defeat recurrence." | Methodological Rigor / Traceability |
| SM-004-iter5 | No quoted example verdict despite citing exact evidence files by path; the panel-file format is entirely narrated | Major | L1 items 1-2 describe verdict structure in prose and cite paths like `.../iteration-009/verify/s-001-refutation-factual.md` without quoting content | Add a 3-5 line quoted excerpt (e.g., the RT-001-iter009 VERIFIED verdict summary row) as a worked example, labeled "illustrative, not the S-016 template text itself" | Completeness / Evidence Quality / Actionability |
| SM-005-iter5 | The old-protocol-to-verified-protocol switch (D-4/Fig. 3) triggers an order-of-magnitude cost jump with no user-notification checkpoint | Major | Fig. 3: "No: fresh stream every round -> SWITCH: Switch to VERIFIED protocol" -- routes automatically, no escalate/notify step, unlike the RT-M-010-ceiling path which explicitly escalates to the user | Add: "The switch decision SHOULD be logged and surfaced to the user/owner before the next round runs, given the ~10x-100x per-round cost increase (Cost model); this is a notification, not an approval gate, so it does not block convergence." | Methodological Rigor / Traceability |
| SM-006-iter5 | RSK-7's "same reviewer roster" claim is asserted without a citation, unlike the rest of RSK-7's carefully evidenced caveats | Minor | RSK-7: "the entire record is n=2 governance/ADR-genre packages, same author role, same reviewer roster, same project, days apart" | Add a citation to the two threads' `adv-selector` strategy-set invocations (or note "same 9-strategy Group A-E finder set selected in both threads") to ground "same reviewer roster" the way the rest of the sentence is grounded | Evidence Quality / Traceability |

---

## Improvement Details

### SM-001-iter5 -- Partial-panel fallback undefined

**Affected Dimension:** Methodological Rigor / Actionability

**Original Content:** The D-1 decision row and L1 item 1 specify "2-of-3 majority, DEFAULT-REFUTED, blind to each other" and "Default rule: **REFUTED on uncertainty** (the anti-inflation default)" (deliverable lines 487, 736), but neither addresses what happens if one of the three lens invocations simply fails to complete (agent error, tool failure, context exhaustion mid-invocation). Since a real implementation (WI-1) will need to handle this case, and DEFAULT-REFUTED is a *content* uncertainty rule ("the claim is uncertain"), it is not self-evidently the same as an *availability* failure rule ("the lens never rendered a verdict at all").

**Strengthened Content:** "A lens invocation that errors, times out, or fails to return a verdict for a given claimed Critical counts as a REFUTED vote for that lens (an extension of the DEFAULT-REFUTED anti-inflation default to lens *unavailability*, not only lens *uncertainty*); the remaining two lenses' verdicts still determine the 2-of-3 majority. A report in which 2 of 3 lenses fail to return is treated as fully REFUTED and flagged for a runner-initiated re-run rather than silently defaulting to VERIFIED or REFUTED on a 1-vote basis."

**Rationale:** This closes an edge case that WI-1's implementer would otherwise have to invent unaided, and it is a one-sentence addition consistent with the ADR's own DEFAULT-REFUTED philosophy (discard-bias, not invent-a-new-rule) -- it does not touch any of D-1 through D-6's chosen options.

**Best Case Conditions:** Applies whenever the adv-verifier agent is actually implemented (WI-1) and a real invocation fails; without it, WI-1's acceptance criteria (currently silent on this) would under-specify a real operational scenario.

---

### SM-002-iter5 -- Dual-protocol sunset trigger lacks the numeric concreteness applied elsewhere

**Affected Dimension:** Actionability / Internal Consistency

**Original Content:** RSK-6's mitigation (deliverable line ~947) reads: "Operative verdict always labeled; sunset the old-protocol composite once the team is calibrated." Elsewhere in the same document (L2 Architectural Implications, deliverable lines ~865-867), an directly analogous transition decision is given a precise, falsifiable trigger: "Trigger: open Phase 2 as a work item if RSK-1/RSK-2 residual exposure... is observed in >= 1 of the first 3 post-ratification C3/C4 tournaments." The document clearly knows how to write a concrete trigger; RSK-6 is the one transition-management clause that does not get one.

**Strengthened Content:** "Operative verdict always labeled; sunset the old-protocol composite once N consecutive C3/C4 rounds (suggest N=3, mirroring the Phase-2 evaluation window already used in this ADR) show no material divergence (e.g., < 0.05 composite delta) between the verified and old-protocol scores, or once the team affirmatively opts to drop dual reporting -- whichever comes first."

**Rationale:** Consistency with the document's own demonstrated standard for transition triggers (numeric, falsifiable) rather than a vaguer "once calibrated" test that a future runner would have to interpret from scratch. This is a genuine strengthening opportunity precisely because the ADR proves, elsewhere in its own text, that it holds itself to a higher bar than this one clause currently meets.

**Best Case Conditions:** Most valuable once WI-3 (dual-protocol reporting) ships and the team is actually deciding, round over round, whether to keep reporting both composites.

---

### SM-003-iter5 -- "Recurrence across independent rounds" is illustrated, not operationally defined

**Affected Dimension:** Methodological Rigor / Traceability

**Original Content:** D-4's chosen option (deliverable lines 418, 490) and its rationale give one worked example of recurrence -- "the grandfather-exemption seam re-derived by 4 independent strategies" (deliverable line ~427-428) -- and WI-8's acceptance criteria (deliverable line 970) ask for "a recurrence-signature check (does a C3 blind rotation reproduce the fresh-stream vs. recurrence pattern...)" without ever stating, in one place, the actual matching rule a disposition-table owner or runner-guide author would apply to decide "is finding X in round N the same recurring item as finding Y in round N-1, or a fresh one?"

**Strengthened Content:** Add, near the D-4 decision row or as a new sentence in the L1 change-surface item for WI-6 (the runner guide): "**Recurrence test:** a finding in round N recurs from an earlier round if it cites the same file+line span (or a materially overlapping span) and names the same underlying defect class, even when the wording, finding ID, or originating strategy differs (the grandfather-seam example above was recurrence across 4 *different* strategies, not the same finding ID repeated). A finding that cites a different location or a different defect class, even if superficially similar in theme, is a fresh (non-recurring) finding."

**Rationale:** This is the single piece of tacit knowledge the 18-round record clearly used (the scorer evidently applied *some* consistent test to distinguish "10 closed, 7 fresh" from "the grandfather seam recurring"), but the ADR never promotes that tacit test into an explicit, transferable rule -- which is exactly the kind of operational definition WI-6 (the runner guide) and WI-8 (the falsification test) need to be executable by someone who was not present for the original 18 rounds.

**Best Case Conditions:** Directly enables WI-8's stated goal of testing whether "C3 needs panels" versus "the panel merely functions at C3" -- that falsification test requires a precise recurrence rule to be applied consistently across the validation rounds.

---

### SM-004-iter5 -- No quoted example verdict despite precise, verified path citations

**Affected Dimension:** Completeness / Evidence Quality / Actionability

**Original Content:** L1 item 1 (deliverable lines 732-735) and item 2 (752-769) describe the verifier's output format and lens rubrics entirely in prose, citing real files by path (e.g., `.../iteration-009/verify/s-001-refutation-factual.md`) but never quoting their content. This review independently confirmed those files exist exactly as described (see Summary verification note) -- so the evidence is available and accurate, it is simply never surfaced in the ADR itself.

**Strengthened Content:** Add, immediately after the L1 item 1 output-format bullet, a short illustrative excerpt such as:

> *Illustrative excerpt (not S-016 template text itself), from `.../iteration-009/verify/s-001-refutation-factual.md`:*
> `RT-001-iter009 -- VERIFIED. Basis: Novel defect: '-path */decisions/*' filter excludes flat docs/design/*.md files (no decisions/ segment exists there); filesystem- and text-confirmed; not covered by any existing R-1..R-17 residual or prior disposition.`

**Rationale:** A single quoted verdict makes the "one file per lens per report, each verdict with a one-paragraph justification and file+line citation" specification (currently only narrated) directly demonstrable, closing the gap between "the mechanism worked" (asserted, and independently confirmed here) and "here is what its output actually looks like" (currently absent). This meaningfully lowers the interpretation burden on whoever implements the S-016 template (WI-2) and the adv-verifier agent (WI-1).

**Best Case Conditions:** Strongest value at WI-2 (template authoring), where a concrete worked example prevents drift between the ADR's narrative description and the template's actual rubric wording.

---

### SM-005-iter5 -- Protocol-switch cost jump has no user-notification checkpoint

**Affected Dimension:** Methodological Rigor / Traceability

**Original Content:** Figure 3 (deliverable lines 626-654) routes a non-convergent fresh-stream signal directly to "SWITCH: Switch to VERIFIED protocol (3-lens refutation panels)" with no escalate/notify step -- contrast this with the RT-M-010-ceiling path in the same diagram, which explicitly routes to "ESCALATE to user." The ADR's own Cost model (deliverable lines 808-819) and Forces #2 ("Independence vs. cost... independence costs ~3 extra agent runs per Critical-bearing report") establish that this switch is not free: it moves the tournament from a old-protocol round (no panels) to a verified-protocol round (an order-of-magnitude more tokens per Critical-bearing report). A decision that changes per-round cost by 10x-100x is exactly the kind of transition the document's own AE-006/RT-M-010 escalation philosophy treats as escalation-worthy elsewhere, but this specific switch point is silent on it.

**Strengthened Content:** Add to Fig. 3's SWITCH node caption or Forces #2: "The switch from old to verified protocol SHOULD be logged and surfaced to the user/owner before the next round is spent, given the substantial per-round cost increase (Cost model); this is a *notification*, not an approval gate -- the tournament proceeds automatically -- so it does not slow convergence, but it prevents the cost jump from being invisible to whoever is budgeting the engagement."

**Rationale:** This is a narrow, non-blocking addition (a log/notify step, not a new approval gate) that brings the one silent cost-changing transition in the pipeline into line with the transparency standard the ADR applies everywhere else (dual-protocol reporting, delta-reconciliation, RT-M-010 escalation). It does not alter D-4's chosen option, only names an existing gap in that option's specification.

**Best Case Conditions:** Matters most for a team budgeting tournament token spend across multiple rounds/packages, where an invisible protocol switch could otherwise appear as an unexplained cost spike.

---

### SM-006-iter5 -- "Same reviewer roster" claim lacks a citation (Minor)

**Affected Dimension:** Evidence Quality / Traceability

**Original Content:** RSK-7 (deliverable line ~948): "the entire record is n=2 governance/ADR-genre packages, same author role, same reviewer roster, same project, days apart (maximally correlated, not merely small-n)." "Same author role" and "same project" are directly verifiable from the ADR's own Context section; "same reviewer roster" is a stronger and more specific claim (that the *same set* of finder strategies/agents ran across both packages) that is not pinned to a citation the way the surrounding claims are.

**Strengthened Content:** Add a short parenthetical, e.g.: "(both threads selected the same Group A-E finder set per `adv-selector.md:109-128`'s recommended order; no package used a materially different strategy roster)."

**Rationale:** Minor because it does not change RSK-7's risk rating or mitigation, and the underlying claim is very plausibly true (both packages ran the standard C4 strategy set per the SSOT). It is flagged only because this is the one clause in an otherwise meticulously-cited risk register that reads as an assertion rather than a citation.

**Best Case Conditions:** Low-cost, high-consistency polish; best folded in alongside any other RSK-7 edit.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-004 closes a "described but not demonstrated" gap in the verifier-output specification |
| Internal Consistency | 0.20 | Positive | SM-002 brings RSK-6's trigger language in line with the document's own Phase-2 trigger precedent |
| Methodological Rigor | 0.20 | Positive | SM-001, SM-003, SM-005 close operational-definition gaps (lens failure, recurrence, cost-transition transparency) that the document's own rigor elsewhere would predict should be present |
| Evidence Quality | 0.15 | Positive | SM-004 and SM-006 add quoted/cited grounding where prose currently stands unquoted or uncited; independent verification during this pass (Summary note) confirms the existing evidence base is otherwise sound |
| Actionability | 0.15 | Positive | SM-001, SM-002, SM-003, SM-004 each remove an interpretation burden from a specific downstream work item (WI-1, WI-2, WI-3, WI-6, WI-8) |
| Traceability | 0.10 | Positive | SM-003, SM-005, SM-006 make implicit tests/decisions (recurrence, switch cost, roster claim) explicit and citable |

**Overall:** No Negative impacts identified -- every improvement strengthens an existing, sound argument rather than exposing a new weakness introduced by this review. Consistent with the charitable reading above, this ADR's core decision (D-1 through D-6) is not challenged by any finding in this report; all six findings are refinements to specification completeness and transition transparency, offered for incorporation before downstream critique strategies (S-002, S-004, S-001) run per H-16.
