# Devil's Advocate Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` (iteration 5, v0.5)
**Criticality:** C3 (per the ADR's own c-007; this review runs the VERIFIED-CRITICALS protocol on itself)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-002 blind pass, iteration 5)
**H-16 Compliance:** Inferred, not directly observed (P-022 label). This agent is BLIND to sibling files under `review/iteration-005/` (including any `s-003-*` output) by task design, so the S-003 Steelman artifact for this specific iteration could not be read. Proceeding is justified by: (a) the tournament's documented 6-group sequential order (self-refine -> steelman -> challenge -> verify -> decompose -> score) is enforced by the orchestrator invoking blind agents in group order, placing Steelman strictly before this Challenge-group (S-002) invocation; (b) the deliverable itself embeds a Steelman-of-every-rejected-option discipline throughout D-1 through D-6 (`.../ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:309-476`), evidencing H-16 practice at the document-construction level across 4 prior iterations. This is an inference, not a confirmed artifact read; flagged per P-022 rather than silently assumed.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Methodology Notes](#methodology-notes) | Steps 1-2 execution record |
| [Findings Table](#findings-table) | All counter-arguments, severity, evidence |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |

---

## Summary

6 counter-arguments identified (1 Critical, 4 Major, 1 Minor), targeting the exact seams the review
brief specified: evidence support for the always-on-vs-conditional verify fork (D-1), token-cost
honesty, whether DEFAULT-REFUTED's false-negative risk is *actually* bounded rather than merely
disclaimed, and the n=2 overfitting exposure. The ADR is unusually self-critical (four prior
remediation iterations, extensive disclosed limitations), which narrowed the available attack surface
considerably -- several initially promising lines (e.g., "is the 2-of-3 majority arbitrary?") turned
out to be already evidenced against by the document itself (materiality-lens case,
`.../ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:918-921`) and were
dropped rather than forced. The one Critical finding (DA-001-iter5) is, however, a genuine and
previously-undisclosed gap: the ADR's own escalation trigger for closing the false-negative risk it
names (RSK-1) depends on an observability capability its own architecture does not provide. Recommend
**REVISE** to address DA-001-iter5 and DA-002-iter5 before this ADR can honestly claim its false-negative
risk is "bounded" rather than merely named.

---

## Methodology Notes

**Step 1 (Role assumption):** Adopted the Devil's Advocate role against
ADR-adversary-tournament-protocol-001 v0.5, C3, per the H-16 inference stated above.

**Step 2 (Assumption inventory, abbreviated):** Explicit assumptions challenged: (a) "independence is
the load-bearing property" (Force 6) -- challenged via RSK-2's own admission that blindness gives
context-independence, not reasoning-independence (DA-006-iter5); (b) "the panel is a reliable
detector of false claims" -- challenged by asking what detects a false *refutation*, not just a false
*confirmation* (DA-001-iter5); (c) "criticality-gating is a defensible cost control" -- challenged via
constraint c-005's evidence-led mandate vs. D-1's own "reasoned default, not an empirical finding"
admission (DA-002-iter5). Implicit assumptions challenged: (d) per-round cost figures are the
decision-relevant unit (DA-003-iter5); (e) the verifier's context budget scales safely with document
size (DA-004-iter5); (f) all three lenses should vote with equal weight (DA-005-iter5).

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter5 | Phase-2 escalation trigger for the false-negative risk (RSK-1) is unobservable under the ADR's own design | Critical | `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:862-867`, `:942`, `:251-253`, `:488` | Internal Consistency |
| DA-002-iter5 | D-1's central always-on-vs-conditional fork admits it is "a reasoned default, not an empirical finding," in tension with the ADR's own evidence-led constraint (c-005) | Major | `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:278`, `:341-344`, `:349-351` | Internal Consistency |
| DA-003-iter5 | Cost model gives only a per-round token figure; no cumulative per-tournament total is computed despite the record showing multiple verified rounds actually ran | Major | `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:808-819`, `:826-838`, `:642`, `:156-219` | Completeness |
| DA-004-iter5 | No stated fallback for citation-dense/large deliverables where a single lens invocation may approach practical context-window limits, per the ADR's own worked cost multiplier | Major | `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:826-838`, `:963` | Actionability |
| DA-005-iter5 | Unweighted 2-of-3 majority treats the materiality lens as equally reliable to the factual-accuracy lens despite the ADR's own admission that materiality is "inherently more subjective" | Major | `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:918-921`, `:487` | Methodological Rigor |
| DA-006-iter5 | WI-8's validation of the C3 boundary and non-ADR-genre generalization is conducted by the same reviewer/model infrastructure that produced the n=2 correlated evidence base, limiting its power to detect calibration (not just functional) failure | Minor | `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:948`, `:943`, `:970` | Evidence Quality |

**Finding ID Format:** `DA-{NNN}-iter5` (execution_id = `iter5`, matching this tournament's own
`DA-NNN-iterN` convention already used throughout the deliverable's changelog, for cross-iteration
stability per this review's citation requirements.)

---

## Finding Details

### DA-001-iter5: Phase-2 escalation trigger is unobservable under the ADR's own design [CRITICAL]

**Claim Challenged:** The L2 Architectural Implications section states the false-negative/correlated-error
risk (RSK-1, RSK-2) is "mitigated, not eliminated, and accepted for now," and names a concrete escalation
path: *"Trigger: open Phase 2 as a work item if RSK-1/RSK-2 residual exposure (a real Critical wrongly
refuted, or a correlated-error false refutation) is observed in >= 1 of the first 3 post-ratification
C3/C4 tournaments"* (`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:865-867`).

**Counter-Argument:** This trigger presupposes a detection capability the protocol itself does not
provide. Per D-2 (`:488`), "Refuted claims (at C3/C4) carry zero dimension weight" -- refuted Criticals
are discarded before they ever reach the owner. The owner-authored disposition table -- the ADR's own
promoted-to-first-class cross-round memory artifact (D-3) -- tags only `CLOSED-BY-DELETION /
CLOSED-BY-EDIT / CLOSED-BY-DISCLOSURE / REBUTTED / RESIDUAL-DISCLOSED` (`:251-253`); there is no
`PANEL-REFUTED` category, and "REBUTTED" in that table denotes the *owner's own* argument against a
finding from the pre-verified-protocol convention, not a panel verdict. So a panel-REFUTED Critical
leaves **no persistent record** anywhere in the tournament's own artifacts. For the team to "observe"
that a refutation was wrong, an independent finder in a *later* round would have to (a) re-raise the
same substantive issue by pure chance of rotation, (b) have it re-panelled from scratch with "no
cross-round memory feeding the panel" (the ADR's own words, RSK-1 mitigation prose, `:942`), and (c) the
result would have to be VERIFIED this time -- and even then, nothing in the design connects that
VERIFIED verdict back to the prior REFUTED one to register it as "the trigger condition just fired."
The one incident the ADR itself uses as proof that independent re-examination works (the fabricated
PR-template claim) was a false *confirmation*, caught by an unrelated blind finder rotation
(`:220-247`) -- the ADR never shows, or even architecturally allows for, the mirror case (a false
*refutation* being caught). The escalation trigger for the ADR's own proposed remediation of this exact
risk therefore depends on an event class its own design renders invisible.

**Evidence:** `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:862-867` (trigger
clause), `:942` (RSK-1 row, "no cross-round memory feeding the panel"), `:251-253` (disposition table
categories, no panel-refuted category), `:488` (D-2 decision row, "carry zero dimension weight").

**Impact:** If this counter-argument holds, RSK-1's stated "MED" probability and the Phase-2 trigger
are not an evidence-gated escalation plan but an unfalsifiable promise -- the condition that would
open Phase 2 cannot occur under the mechanism as specified, so Phase 2 is de facto permanently
deferred regardless of the actual false-negative rate.

**Dimension:** Internal Consistency (the escalation-trigger clause contradicts the discard-and-forget
treatment of refuted claims established two sections earlier in the same document).

**Response Required:** Either (a) add a lightweight persistent record of panel-REFUTED Critical
claims (even a one-line disposition-table entry, e.g. `PANEL-REFUTED`) so a later independent
re-raising of the same substance can be cross-referenced and counted toward the trigger, or (b)
honestly reframe RSK-1's mitigation to state that the residual is *unmonitored*, not merely
"mitigated, not eliminated," and drop the specific Phase-2 trigger condition until an actual
observability mechanism exists.

**Acceptance Criteria:** The next revision either (1) adds a disposition-table category or equivalent
artifact that persists panel-REFUTED Critical claims across rounds for cross-referencing, with the
Phase-2 trigger explicitly keyed to it, or (2) replaces the "observed in >= 1 of the first 3
post-ratification tournaments" trigger with language that discloses the residual as currently
unobservable and states what would need to exist before it *could* be observed.

---

### DA-002-iter5: D-1's central fork is admittedly not evidence-led, in tension with constraint c-005 [MAJOR]

**Claim Challenged:** Constraint c-005 states: *"The decision must be evidence-led and cite the
tournament record"* (`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:278`).
D-1 -- arguably the single highest-leverage fork in the entire ADR (always-on vs. criticality-gated
verification) -- states of its own chosen resolution: *"The choice between B and C, however, rests on
a reasoned default, not an empirical finding"* and that, given the all-C4 evidence base, *"the
'always-on' (B) and 'criticality-gated' (C) options are empirically indistinguishable, so C is
selected on a proportionality argument rather than an observation"* (`:341-344`, `:349-351`).

**Counter-Argument:** The ADR's own self-correction discipline (DA-006-i2, `:312-317`) already
concedes the option scores (9 vs. 6) are "relative preference orderings ... not confidence levels
derived from the (all-C4) evidence base" -- but relabeling a non-evidence-based judgment as a
"preference ordering" does not resolve the tension with c-005; it only names it more precisely.
Constraint c-005 was declared as a *commission-level* requirement governing this ADR's decisions, and
D-1 is not a peripheral decision -- it is the fork the entire ADR is titled after (a "Verified-Criticals
Tournament *Methodology*" whose central mechanism is D-1's verify stage). An ADR that states plainly
"our most consequential choice rests on a reasoned default, not an empirical finding" while operating
under a constraint that "the decision must be evidence-led" has either scoped c-005 too broadly
(applying it to the ADR's overall citation discipline but not to every individual fork) or has
violated it at the one fork where violation matters most. The document does not clarify which reading
is intended.

**Evidence:** `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:278` (c-005),
`:341-344` (D-1 "reasoned default, not an empirical finding"), `:349-351` ("empirically
indistinguishable").

**Impact:** If c-005 is read strictly, D-1's chosen-option rationale is out of compliance with the
ADR's own stated ground rules for how it is allowed to decide anything -- undermining the "evidence-led"
framing the L0 Executive Summary and Rationale sections lean on heavily.

**Dimension:** Internal Consistency.

**Response Required:** Either narrow c-005's scope explicitly (e.g., "the overall methodology must be
evidence-led; individual sub-decisions where the record is silent MUST say so and may use a reasoned
default, disclosed as such") or strengthen D-1's justification with something beyond proportionality
argument -- e.g., an explicit cost-benefit threshold computation using the Cost model's own numbers
(see DA-003-iter5) that at least makes the "reasoned default" a quantified one.

**Acceptance Criteria:** c-005's wording, or D-1's rationale, is revised so the two are not in
apparent conflict on a plain reading of both.

---

### DA-003-iter5: Cost model is per-round only; no whole-tournament aggregate is ever computed [MAJOR]

**Claim Challenged:** *"Per round, cost ~= 3 x (number of Critical-bearing reports) at C4 ... a C4
round with 4-5 such reports therefore runs on the order of 0.4-0.5M input tokens as a floor for the
Verify stage alone"* (`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:808-819`,
`:826-838`).

**Counter-Argument:** The Alignment table claims "Constraint Satisfaction: HIGH ... cost gated by
criticality (c-004)" (implicit reference at the Decision section's Alignment row) and RSK-4 caps
*per-round* cost, but the record the ADR itself cites shows tournaments running *multiple* verified
rounds before reaching a stop condition: ADR-convention iterations 9 and 10, and FU-log iterations 7
and 8, are all named as verified-protocol rounds within the same two tournaments
(`:156-219`). RT-M-010's own ceiling allows up to 7 (C3) or 10 (C4) rounds
(`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:642`). Multiplying the
ADR's own per-round floor (0.4-0.5M tokens) by even 4 rounds -- the actual historical count of
verified-protocol rounds run on a single package -- yields 1.6-2.0M input tokens for the Verify stage
alone across one tournament, a figure the ADR never states. A reader trying to answer "is this
proportionate?" (Force 2, "independence vs. cost") has no whole-tournament number to weigh, only a
per-round snapshot that understates the actual multi-round exposure by 4x or more in the ADR's own
demonstrated worst case.

**Evidence:** `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:808-819` (cost
formula), `:826-838` (token estimate), `:642` (RT-M-010 ceiling), `:156-219` (four verified rounds
actually run).

**Impact:** The "Implementation Effort: M-L aggregate" and "cost gated by criticality" claims in the
Alignment section are not falsifiable against any number the ADR itself provides at the scale a team
would actually budget against (a tournament, not a round).

**Dimension:** Completeness.

**Response Required:** Add a worked per-tournament aggregate (e.g., "N verified rounds x 0.4-0.5M
tokens/round = X-Y total for the Verify stage across a full C4 tournament") using the ADR's own
formula and the historical round counts it already cites, so the cost claim is checkable at the unit
a reader actually cares about.

**Acceptance Criteria:** A per-tournament (not merely per-round) token-cost figure appears in either
the Cost model or the RSK-4 mitigation, derived from the ADR's own formula and at least one of its own
cited round counts.

---

### DA-004-iter5: No stated fallback for citation-dense/large deliverables at the single-invocation level [MAJOR]

**Claim Challenged:** *"True per-report cost may run 2-5x the deliverable-only figure ... this ADR
alone cites ~18 evidence files, several substantial"*
(`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:826-838`).

**Counter-Argument:** Applying the ADR's own multiplier to its own per-lens deliverable-only estimate
(roughly ~35k tokens per lens for a document this size, per the "3 x ~35k" breakdown at `:829`) implies
a single `adv-verifier` lens invocation on a citation-dense document of this class could plausibly run
into the low-to-mid hundreds of thousands of input tokens once cited-evidence reload is counted --
approaching or exceeding common single-context-window budgets for such invocations. Neither the L1
Technical Implementation section's `adv-verifier` contract nor WI-1's acceptance criteria
(`:963`) mention any behavior for this case -- no evidence-subset prioritization, no chunked reading
strategy, no explicit "if the report + evidence set exceeds budget X, do Y" fallback. The agent's own
governing framework already tracks context budget as a first-class concern
(`agent-development-standards.md` CB-01-CB-05, cited by this very ADR at `:835-836`), so the omission
is not a matter of the concept being foreign to the framework -- it is specifically absent from this
agent's own specification, for exactly the deliverable class (citation-dense governance ADRs) the ADR
identifies as its own worst case.

**Evidence:** `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:826-838` (2-5x
multiplier, 18 cited files), `:963` (WI-1 acceptance criteria, no budget-fallback clause).

**Impact:** WI-1 is not fully implementable as specified for the exact deliverable class the ADR uses
to justify its own cost estimates; a builder would have to invent this behavior unguided, risking
silent truncation or incomplete adjudication for large, citation-dense reports.

**Dimension:** Actionability.

**Response Required:** Add an explicit fallback clause to WI-1's acceptance criteria (or the L1
`adv-verifier` contract) specifying behavior when a report's deliverable + cited-evidence set exceeds
a stated token budget (e.g., prioritize the deliverable and the specific cited lines over full file
reads, or split the report's Criticals across multiple invocations).

**Acceptance Criteria:** WI-1's acceptance criteria or the L1 `adv-verifier` contract names a concrete
behavior for the large/citation-dense case, not merely a cost estimate acknowledging the case exists.

---

## Recommendations

**P0 (Critical -- MUST resolve before acceptance):**
- **DA-001-iter5:** Add a persistent record for panel-REFUTED Criticals (or reframe the Phase-2
  trigger as currently unobservable) before this ADR can claim RSK-1's residual is monitored rather
  than merely disclaimed. Acceptance criteria: see Finding Details.

**P1 (Major -- SHOULD resolve; require justification if not):**
- **DA-002-iter5:** Reconcile c-005's "evidence-led" mandate with D-1's "reasoned default, not an
  empirical finding" admission -- narrow the constraint's scope or strengthen D-1's rationale.
- **DA-003-iter5:** Add a whole-tournament (not just per-round) token-cost aggregate using the ADR's
  own formula and cited round counts.
- **DA-004-iter5:** Add an explicit context-budget fallback clause to WI-1's acceptance criteria for
  citation-dense/large deliverables.
- **DA-005-iter5:** Either justify unweighted lens voting despite the acknowledged materiality-lens
  subjectivity gap, or introduce an asymmetric rule (e.g., factual-lens agreement as a necessary
  condition).

**P2 (Minor -- MAY resolve; acknowledgment sufficient):**
- **DA-006-iter5:** Acknowledge in RSK-7 or WI-8's acceptance criteria that the validation
  infrastructure shares a potential bias source with the original evidence base, limiting WI-8 to
  detecting gross functional failure rather than calibration miscalibration.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-003-iter5: no whole-tournament cost aggregate despite the record showing multi-round verified tournaments actually occurred |
| Internal Consistency | 0.20 | Negative | DA-001-iter5: escalation trigger contradicts the discard-and-forget treatment of refuted claims; DA-002-iter5: c-005 vs. D-1's own non-evidence-based admission |
| Methodological Rigor | 0.20 | Negative | DA-005-iter5: equal-weight lens voting not evaluated against alternatives despite the ADR's own evidence of differential lens reliability |
| Evidence Quality | 0.15 | Negative | DA-006-iter5: WI-8's validation instrument shares a bias source with the evidence it is meant to validate against |
| Actionability | 0.15 | Negative | DA-004-iter5: WI-1 acceptance criteria omit a fallback for the citation-dense case the ADR's own cost model flags as its worst case |
| Traceability | 0.10 | Neutral | All findings trace to specific cited lines within the deliverable; no traceability gap identified by this pass |

**Overall assessment:** Targeted revision required. None of the six findings invalidates the chosen
mechanism (D-1 through D-6 remain the best-supported options among those considered); DA-001-iter5 is
the one finding that, left unaddressed, would let the ADR overstate how well its own named residual
risk is actually being managed.

---

**Generated by:** adv-executor (S-002 Devil's Advocate)
**Template:** `.context/templates/adversarial/s-002-devils-advocate.md` v1.0.0
